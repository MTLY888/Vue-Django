# evaluation/urls.py

from django.urls import path
from . import views

# 这个文件定义了所有后端API的路由。
# 每个URL路径都映射到一个在 views.py 中定义的视图函数。
urlpatterns = [
    # --- 基础模型评估 ---
    path('accuracy-test/', views.start_accuracy_test, name='start_accuracy_test'),
    path('transfer-test/', views.start_transfer_test, name='transfer_test'),
    path('robust-test/', views.start_robust_test, name='robust_test'),

    # --- 数据质量评估 ---
    path('data-quality/', views.start_data_quality_evaluation, name='start_data_quality_evaluation'),
    path('quality-images/<str:url_prefix>/<str:filename>', views.serve_quality_image, name='serve_quality_image'),

    # --- 数据信息量评估 ---
    path('data-info/start/', views.start_data_info_evaluation, name='start_data_info_evaluation'),
    path('data-info/results/', views.get_data_info_results, name='get_data_info_results'),
     # 数据信息量评估图片服务 - 更新为正确的、简化的路径
    path('data-info/<str:image_type>/<str:model_name>/<str:dataset_name>/<str:folder_name>/<str:image_name>',
         views.serve_data_info_image,
         name='serve_data_info_image'),
   

    # --- 特征重要性评估 ---
    path('feature-importance/start/', views.start_feature_importance_evaluation, name='feature_importance_start'),
    path('feature-importance/images/', views.get_feature_importance_images, name='feature_importance_images'),
    path('feature-importance/chart/<str:chart_type>/<str:filename>', views.serve_feature_importance_chart, name='serve_feature_importance_chart'),
    path('feature-importance/image/<str:noise_type>/<str:filename>', views.serve_feature_importance_image, name='serve_feature_importance_image'),

    # --- 对抗性差异可解释性 ---
    path('adversarial/start/', views.start_adversarial_evaluation, name='start_adversarial_evaluation'),
    path('adversarial/images/', views.get_adversarial_images, name='get_adversarial_images'),
    path('adversarial/features/', views.get_adversarial_features, name='get_adversarial_features'),
    path('adversarial/features/more/', views.get_more_adversarial_features, name='get_more_adversarial_features'),
    path('adversarial/feature/difference/', views.calculate_single_feature_difference, name='calculate_single_feature_difference'),
    path('adversarial/image/<str:image_type>/<str:filename>', views.serve_adversarial_image, name='serve_adversarial_image'),

    # --- 因果特征分析 ---
    path('causal-feature/start/', views.start_causal_feature_evaluation, name='start_causal_feature_evaluation'),
    path('causal-feature/images/', views.get_causal_feature_images, name='get_causal_feature_images'),
    path('causal-feature/details/', views.get_causal_feature_details, name='get_causal_feature_details'),
    path('causal-feature/features-batch/', views.get_causal_features_batch, name='get_causal_features_batch'),
    path('causal-feature/effect/', views.calculate_causal_feature_effect, name='calculate_causal_feature_effect'),
    path('causal-feature/distribution/', views.get_causal_effect_distribution, name='get_causal_effect_distribution'),
    path('causal-feature/image/<str:image_type>/<str:filename>', views.serve_causal_feature_image, name='serve_causal_feature_image'),

    # --- 高斯平滑分析 ---
    path('gaussian-smoothing/start/', views.start_gaussian_smoothing_evaluation, name='start_gaussian_smoothing_evaluation'),
    path('gaussian-smoothing/images/', views.get_gaussian_smoothing_images, name='get_gaussian_smoothing_images'),
    path('gaussian-smoothing/details/', views.get_gaussian_smoothing_details, name='get_gaussian_smoothing_details'),
    path('gaussian-smoothing/image/<str:image_type>/<path:file_path>', views.serve_gaussian_smoothing_image, name='serve_gaussian_smoothing_image'),

    # --- 卷积功能分解 ---
    path('convolution-decomposition/start/', views.start_convolution_decomposition_evaluation, name='start_convolution_decomposition_evaluation'),
    path('convolution-decomposition/results/', views.get_convolution_decomposition_results, name='get_convolution_decomposition_results'),
    path('convolution-decomposition/images/', views.get_convolution_decomposition_images, name='get_convolution_decomposition_images'),
    path('convolution-decomposition/predictions/', views.get_convolution_prediction_images, name='get_convolution_prediction_images'),
    
    # 图片服务路径
    # 原图服务
    path('convolution-decomposition/image/original/<str:filename>', views.serve_convolution_original_image, name='serve_convolution_original_image'),
    
    # 图表服务
    path('convolution-decomposition/chart/<str:folder_or_filename>/<str:filename>', views.serve_convolution_decomposition_image, {'image_type': 'chart'}, name='serve_convolution_chart'),
    
    # 预测图片服务 - 使用专门的函数
    path('convolution-decomposition/image/prediction/<str:folder>/<str:filename>', views.serve_convolution_prediction_image, name='serve_convolution_prediction_image'),

    # 在 evaluation/urls.py 文件中添加以下路由

    # --- 概念敏感性分析 ---
    path('concept-sensitivity/start/', views.start_concept_sensitivity_evaluation, name='start_concept_sensitivity_evaluation'),
    path('concept-sensitivity/results/', views.get_concept_sensitivity_results, name='get_concept_sensitivity_results'),
    path('concept-sensitivity/images/', views.get_concept_sensitivity_images, name='get_concept_sensitivity_images'),
    path('concept-sensitivity/prediction/', views.get_concept_sensitivity_prediction, name='get_concept_sensitivity_prediction'),

   # 在 evaluation/urls.py 文件中，将概念敏感性部分的URL模式替换为以下内容：

    # --- 概念敏感性分析 ---
    path('concept-sensitivity/start/', views.start_concept_sensitivity_evaluation, name='start_concept_sensitivity_evaluation'),
    path('concept-sensitivity/results/', views.get_concept_sensitivity_results, name='get_concept_sensitivity_results'),
    path('concept-sensitivity/images/', views.get_concept_sensitivity_images, name='get_concept_sensitivity_images'),
    path('concept-sensitivity/prediction/', views.get_concept_sensitivity_prediction, name='get_concept_sensitivity_prediction'),

    # 概念敏感性图片服务路径 - 修复后
    # 原图服务
    path('concept-sensitivity/image/original/<str:data_folder>/<str:filename>', views.serve_concept_sensitivity_image, name='serve_concept_sensitivity_original_image'),

    # 概念图像服务 - 修复：将image_type包含在URL路径中
    path('concept-sensitivity/image/concept/<str:concept_name>', views.serve_concept_sensitivity_image, name='serve_concept_sensitivity_concept_image'),

    # 概念边界服务
    path('concept-sensitivity/image/concept-boundary/<str:result_folder>/<str:concept_filename>', views.serve_concept_sensitivity_image, name='serve_concept_sensitivity_boundary'),

    # 样本梯度服务
    path('concept-sensitivity/image/sample-gradient/<str:result_folder>/<str:filename>', views.serve_concept_sensitivity_image, name='serve_concept_sensitivity_gradient'),

    # 图表服务
    path('concept-sensitivity/chart/<str:result_folder>/<str:filename>', views.serve_concept_sensitivity_image, name='serve_concept_sensitivity_chart'),
    
    # --- 结构层次化分析 ---
    path('structural-hierarchy/start/', views.start_structural_hierarchy_evaluation, name='start_structural_hierarchy_evaluation'),
    path('structural-hierarchy/results/', views.get_structural_hierarchy_results, name='get_structural_hierarchy_results'),
    path('structural-hierarchy/images/', views.get_structural_hierarchy_images, name='get_structural_hierarchy_images'),
    path('structural-hierarchy/features/', views.get_structural_hierarchy_features, name='get_structural_hierarchy_features'),
    
    # 结构层次化图片服务路径
    # 原图服务
    path('structural-hierarchy/image/original/<str:file_path>', views.serve_structural_hierarchy_image, {'image_type': 'original'}, name='serve_structural_hierarchy_original'),
    
    # 图表服务（包括趋势图）
    path('structural-hierarchy/chart/<path:file_path>', views.serve_structural_hierarchy_image, {'image_type': 'chart'}, name='serve_structural_hierarchy_chart'),

]