# UT_physicians_2

DB considerations:
1. get rid of AppointmentSlots - too many things to load
2. have the appointment carry the referring provider and referral number - patients can have multiple appointment with different clinics from different providers. Creates scalability issues. 
3. Since no more AppointmentSlot, we will have to create all appointments to be preloaded.
4. Create two appointment for each time slot at each location. Will have green, yellow, red for 2, 1, and no appointments left. 
  
Twilio Considerations:
  1. Need to upgrade account to implement fax resource
  2. click to call functionality
  3. appointment reminders

Google Maps locator
https://developers.google.com/maps/solutions/store-locator/clothing-store-locator