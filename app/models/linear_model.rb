class LinearModel
  include MongoMapper::Document

  key :class1, String
  key :class2, String
  key :model, Hash

  LinearModel.ensure_index [[:class1, 1], [:class2, -1]], :unique => true

end
