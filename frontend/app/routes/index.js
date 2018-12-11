import Ember from 'ember';
import RSVP from 'rsvp';


export default Ember.Route.extend({
  model() {
    return RSVP.hash({
      events: this.store.findAll('event'),
      groups: this.store.findAll('group'),
      children: this.store.findAll('child'),
      profiles: this.store.findAll('profile'),
      users: this.store.findAll('user')
    });
  }
	// model() {
  //   return this.store.findAll("group");
  //
  // }

});
