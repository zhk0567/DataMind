"""
时间序列分析模块
提供ARIMA、指数平滑、平稳性检验等功能
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from scipy import stats
try:
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
    from statsmodels.stats.diagnostic import acorr_ljungbox
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False


class TimeSeriesAnalyzer:
    """时间序列分析类"""
    
    @staticmethod
    def analyze_trend_seasonality(
        df: pd.DataFrame,
        time_column: str,
        value_column: str
    ) -> Dict[str, Any]:
        """
        分析时间序列的趋势和季节性
        
        参数:
            df: 数据框
            time_column: 时间列
            value_column: 数值列
        """
        if time_column not in df.columns or value_column not in df.columns:
            raise ValueError("时间列或数值列不存在")
        
        # 确保时间列为datetime类型
        df = df.copy()
        df[time_column] = pd.to_datetime(df[time_column])
        df = df.sort_values(time_column)
        
        values = df[value_column].dropna().values
        time_index = df[time_column].dropna()
        
        if len(values) < 2:
            return {'error': '数据点不足'}
        
        # 趋势分析（线性回归）
        x = np.arange(len(values))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
        
        # 季节性分析（如果数据足够）
        seasonal_info = {}
        if len(values) >= 12:
            # 尝试检测月度季节性
            if len(values) >= 24:
                # 计算月度平均值
                monthly_avg = []
                for i in range(12):
                    month_values = [values[j] for j in range(i, len(values), 12)]
                    if month_values:
                        monthly_avg.append(np.mean(month_values))
                
                if monthly_avg:
                    seasonal_variance = np.var(monthly_avg)
                    seasonal_info['monthly_seasonality'] = {
                        'variance': float(seasonal_variance),
                        'has_seasonality': seasonal_variance > np.var(values) * 0.1
                    }
        
        return {
            'trend': {
                'slope': float(slope),
                'intercept': float(intercept),
                'direction': '上升' if slope > 0 else '下降' if slope < 0 else '平稳',
                'r_squared': float(r_value ** 2),
                'p_value': float(p_value)
            },
            'seasonality': seasonal_info,
            'basic_stats': {
                'mean': float(np.mean(values)),
                'std': float(np.std(values)),
                'min': float(np.min(values)),
                'max': float(np.max(values))
            }
        }
    
    @staticmethod
    def test_stationarity(
        df: pd.DataFrame,
        value_column: str,
        test_type: str = 'adf'
    ) -> Dict[str, Any]:
        """
        平稳性检验
        
        参数:
            df: 数据框
            value_column: 数值列
            test_type: 检验类型 ('adf', 'kpss')
        """
        if not STATSMODELS_AVAILABLE:
            raise ImportError("需要安装statsmodels库以使用平稳性检验")
        
        if value_column not in df.columns:
            raise ValueError("数值列不存在")
        
        values = df[value_column].dropna().values
        
        if len(values) < 10:
            return {'error': '数据点不足，至少需要10个数据点'}
        
        if test_type == 'adf':
            # ADF检验（Augmented Dickey-Fuller）
            result = adfuller(values)
            return {
                'test_type': 'ADF',
                'test_statistic': float(result[0]),
                'p_value': float(result[1]),
                'critical_values': {f'level_{k}': float(v) for k, v in result[4].items()},
                'is_stationary': result[1] < 0.05,
                'interpretation': '平稳' if result[1] < 0.05 else '非平稳'
            }
        
        elif test_type == 'kpss':
            # KPSS检验
            result = kpss(values, regression='c')
            return {
                'test_type': 'KPSS',
                'test_statistic': float(result[0]),
                'p_value': float(result[1]),
                'critical_values': {f'level_{k}': float(v) for k, v in result[3].items()},
                'is_stationary': result[1] > 0.05,
                'interpretation': '平稳' if result[1] > 0.05 else '非平稳'
            }
        
        else:
            raise ValueError(f"不支持的检验类型: {test_type}")
    
    @staticmethod
    def fit_arima(
        df: pd.DataFrame,
        value_column: str,
        order: Tuple[int, int, int] = (1, 1, 1),
        seasonal_order: Optional[Tuple[int, int, int, int]] = None
    ) -> Dict[str, Any]:
        """
        拟合ARIMA模型
        
        参数:
            df: 数据框
            value_column: 数值列
            order: ARIMA阶数 (p, d, q)
            seasonal_order: 季节性ARIMA阶数 (P, D, Q, s)
        """
        if not STATSMODELS_AVAILABLE:
            raise ImportError("需要安装statsmodels库以使用ARIMA模型")
        
        if value_column not in df.columns:
            raise ValueError("数值列不存在")
        
        values = df[value_column].dropna().values
        
        if len(values) < max(order) * 2 + 5:
            return {'error': '数据点不足'}
        
        try:
            if seasonal_order:
                model = ARIMA(values, order=order, seasonal_order=seasonal_order)
            else:
                model = ARIMA(values, order=order)
            
            fitted_model = model.fit()
            
            # 预测
            forecast_steps = min(10, len(values) // 4)
            forecast = fitted_model.forecast(steps=forecast_steps)
            forecast_ci = fitted_model.get_forecast(steps=forecast_steps).conf_int()
            
            return {
                'model_type': 'ARIMA' + ('(S)' if seasonal_order else ''),
                'order': order,
                'seasonal_order': seasonal_order,
                'aic': float(fitted_model.aic),
                'bic': float(fitted_model.bic),
                'forecast': forecast.tolist(),
                'forecast_ci_lower': forecast_ci.iloc[:, 0].tolist(),
                'forecast_ci_upper': forecast_ci.iloc[:, 1].tolist(),
                'residuals': fitted_model.resid.tolist(),
                'summary': str(fitted_model.summary())
            }
        except Exception as e:
            return {'error': f'ARIMA模型拟合失败: {str(e)}'}
    
    @staticmethod
    def exponential_smoothing(
        df: pd.DataFrame,
        value_column: str,
        trend: Optional[str] = None,
        seasonal: Optional[str] = None,
        seasonal_periods: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        指数平滑
        
        参数:
            df: 数据框
            value_column: 数值列
            trend: 趋势类型 ('add', 'mul', None)
            seasonal: 季节性类型 ('add', 'mul', None)
            seasonal_periods: 季节性周期
        """
        if not STATSMODELS_AVAILABLE:
            raise ImportError("需要安装statsmodels库以使用指数平滑")
        
        if value_column not in df.columns:
            raise ValueError("数值列不存在")
        
        values = df[value_column].dropna().values
        
        if len(values) < 10:
            return {'error': '数据点不足'}
        
        try:
            model = ExponentialSmoothing(
                values,
                trend=trend,
                seasonal=seasonal,
                seasonal_periods=seasonal_periods
            )
            fitted_model = model.fit()
            
            # 预测
            forecast_steps = min(10, len(values) // 4)
            forecast = fitted_model.forecast(steps=forecast_steps)
            
            return {
                'model_type': 'Exponential Smoothing',
                'trend': trend,
                'seasonal': seasonal,
                'seasonal_periods': seasonal_periods,
                'aic': float(fitted_model.aic),
                'bic': float(fitted_model.bic),
                'forecast': forecast.tolist(),
                'fitted_values': fitted_model.fittedvalues.tolist(),
                'residuals': (values - fitted_model.fittedvalues).tolist()
            }
        except Exception as e:
            return {'error': f'指数平滑模型拟合失败: {str(e)}'}
    
    @staticmethod
    def compute_acf_pacf(
        df: pd.DataFrame,
        value_column: str,
        nlags: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        计算自相关函数(ACF)和偏自相关函数(PACF)
        
        参数:
            df: 数据框
            value_column: 数值列
            nlags: 滞后期数
        """
        if not STATSMODELS_AVAILABLE:
            raise ImportError("需要安装statsmodels库以使用ACF/PACF")
        
        if value_column not in df.columns:
            raise ValueError("数值列不存在")
        
        values = df[value_column].dropna().values
        
        if len(values) < 10:
            return {'error': '数据点不足'}
        
        if nlags is None:
            nlags = min(40, len(values) // 4)
        
        # 计算ACF和PACF
        acf_values, acf_confint = acf(values, nlags=nlags, alpha=0.05, fft=True)
        pacf_values, pacf_confint = pacf(values, nlags=nlags, alpha=0.05)
        
        return {
            'acf': acf_values.tolist(),
            'acf_confidence_intervals': acf_confint.tolist(),
            'pacf': pacf_values.tolist(),
            'pacf_confidence_intervals': pacf_confint.tolist(),
            'nlags': nlags
        }
    
    @staticmethod
    def white_noise_test(
        df: pd.DataFrame,
        value_column: str,
        lags: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        白噪声检验（Ljung-Box检验）
        
        参数:
            df: 数据框
            value_column: 数值列
            lags: 滞后期数
        """
        if not STATSMODELS_AVAILABLE:
            raise ImportError("需要安装statsmodels库以使用白噪声检验")
        
        if value_column not in df.columns:
            raise ValueError("数值列不存在")
        
        values = df[value_column].dropna().values
        
        if len(values) < 10:
            return {'error': '数据点不足'}
        
        if lags is None:
            lags = min(10, len(values) // 4)
        
        try:
            result = acorr_ljungbox(values, lags=lags, return_df=True)
            
            return {
                'test_statistic': result['lb_stat'].tolist(),
                'p_value': result['lb_pvalue'].tolist(),
                'lags': list(range(1, lags + 1)),
                'is_white_noise': (result['lb_pvalue'] > 0.05).all(),
                'interpretation': '是白噪声' if (result['lb_pvalue'] > 0.05).all() else '不是白噪声'
            }
        except Exception as e:
            return {'error': f'白噪声检验失败: {str(e)}'}

