import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr("string"),
  phonenumber: DS.attr("number"),
  user: DS.belongsTo("user", {async: true})

});
