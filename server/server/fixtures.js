// There's probably a better way of doing fixtures...
Meteor.startup(function () {
    if (Bathrooms.find().count() === 0 && Stalls.find().count() === 0) {
        var stall1 = Stalls.insert({num: 1, occupied: true});
        var stall2 = Stalls.insert({num: 2, occupied: false});
        Bathrooms.insert({description: "Biggie", stalls: [stall1, stall2]});
    }
});
