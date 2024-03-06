odoo.define("helpdesk_mgmt.portal", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");

    publicWidget.registry.PortalHomeCounters.include({
        /**
         * @override
         */
        _getCountersAlwaysDisplayed() {
         // We want to always show the tickets entry
            return this._super(...arguments).concat(["ticket_count"]);
        },
    });
});
