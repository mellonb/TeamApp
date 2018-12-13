import Ember from 'ember';
import {
 add,
 isBefore,
 startOf,
 endOf,
 isoWeekday,
 weekday
} from "ember-power-calendar-utils";

export default Ember.Controller.extend({
   collection: [],
   eventsdidload:Ember.observer("model.events", function(){
     let events = this.get("model.events");
     let collection = this.get("collection")
     events.forEach(function(event){
       collection.push(event.get("timestamp"))
     })
   }),
//    days: Ember.computed(function() {
//      let now = new Date();
//      let day = startOf(startOf(now, "month"), "isoWeekday");
//      let lastDay = endOf(endOf(now, "month"), "isoWeekday");
//      let days = [];
//      while (isBefore(day, lastDay)) {
//        if (weekday(day) !== 1 && weekday(day) !== 3) { // Skip Mon/Wed
//          let copy = new Date(day);
//          let isCurrentMonth = copy.getMonth() === now.getMonth();
//          days.push({
//            date: copy,
//            isCurrentMonth
//          });
//        }
//        day = add(day, 1, "day");
//      }
//      return days;
//    }),
//    weeksWithoutMondaysOrWednesday: Ember.computed('noMondays', function() {
//   let days = this.get('days');
//   let weeks = [];
//   let i = 0;
//   while (days[i]) {
//     weeks.push({ days: days.slice(i, i + 5) });
//     i += 5;
//   }
//   return weeks;
// })




});
