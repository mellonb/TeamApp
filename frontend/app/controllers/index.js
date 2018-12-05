import Ember from 'ember';

export default Ember.Controller.extend({
  testmath: Ember.computed('', function(){
    return 1+1;
  })
});
