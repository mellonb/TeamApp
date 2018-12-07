import DS from 'ember-data';

export default DS.Model.extend({
  timestamp: DS.attr("date"),
  title: DS.attr("string"),
  info: DS.attr("string"),
  group: DS.belongsTo("group", {async: true})
});
