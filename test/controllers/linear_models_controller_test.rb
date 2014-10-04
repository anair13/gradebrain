require 'test_helper'

class LinearModelsControllerTest < ActionController::TestCase
  setup do
    @linear_model = linear_models(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:linear_models)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create linear_model" do
    assert_difference('LinearModel.count') do
      post :create, linear_model: { class1: @linear_model.class1, class2: @linear_model.class2, model: @linear_model.model }
    end

    assert_redirected_to linear_model_path(assigns(:linear_model))
  end

  test "should show linear_model" do
    get :show, id: @linear_model
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @linear_model
    assert_response :success
  end

  test "should update linear_model" do
    patch :update, id: @linear_model, linear_model: { class1: @linear_model.class1, class2: @linear_model.class2, model: @linear_model.model }
    assert_redirected_to linear_model_path(assigns(:linear_model))
  end

  test "should destroy linear_model" do
    assert_difference('LinearModel.count', -1) do
      delete :destroy, id: @linear_model
    end

    assert_redirected_to linear_models_path
  end
end
