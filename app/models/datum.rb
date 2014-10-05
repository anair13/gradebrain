require 'json'

class Datum
  include MongoMapper::Document
  validates_presence_of :input, :message => 'Input cannot be empty'
  validate :json_format
  key :input, String
  key :academics, Hash
  key :academics_hash, Integer

  Datum.ensure_index :academics_hash, :unique => true

  before_save :parse_input

  private
  def parse_input
    @academics = JSON.parse(@input)
    @academics_hash = @academics.to_s.hash
  end

  def json_format
    errors[:base] << "not in json format" unless JSON.is_json?(@input)
  end

end