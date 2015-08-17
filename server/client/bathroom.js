Template.bathroom.helpers({
    get_stall: function(id) {
        return Stalls.findOne({_id: id});
    }
})