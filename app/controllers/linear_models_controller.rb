class LinearModelsController < ApplicationController
  before_action :set_linear_model, only: [:show, :edit, :update, :destroy]

  # GET /linear_models
  # GET /linear_models.json
  def index
    @linear_models = LinearModel.all
  end

  # GET /linear_models/1
  # GET /linear_models/1.json
  def show
  end

  def get_model
    @linear_model = LinearModel.find_by_class1_and_class2(params[:class1], params[:class2])
    if @linear_model
      render :json => @linear_model.model
    else
      render :json => {}
    end
  end

  # GET /linear_models/new
  def new
    @linear_model = LinearModel.new
  end

  # GET /linear_models/1/edit
  def edit
  end

  # POST /linear_models
  # POST /linear_models.json
  def create
    @linear_model = LinearModel.new(linear_model_params)

    respond_to do |format|
      if @linear_model.save
        format.html { redirect_to @linear_model, notice: 'Linear model was successfully created.' }
        format.json { render action: 'show', status: :created, location: @linear_model }
      else
        format.html { render action: 'new' }
        format.json { render json: @linear_model.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /linear_models/1
  # PATCH/PUT /linear_models/1.json
  def update
    respond_to do |format|
      if @linear_model.update(linear_model_params)
        format.html { redirect_to @linear_model, notice: 'Linear model was successfully updated.' }
        format.json { head :no_content }
      else
        format.html { render action: 'edit' }
        format.json { render json: @linear_model.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /linear_models/1
  # DELETE /linear_models/1.json
  def destroy
    @linear_model.destroy
    respond_to do |format|
      format.html { redirect_to linear_models_url }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_linear_model
      @linear_model = LinearModel.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def linear_model_params
      params.require(:linear_model).permit(:class1, :class2, :model)
    end
end
