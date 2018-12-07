import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr("string"),
  phone_number: DS.attr("number"),
  user: DS.belongsTo("profile", {async: true})

});
