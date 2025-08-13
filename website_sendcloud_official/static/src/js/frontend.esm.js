/* global sendcloud */
import { KeepLast } from "@web/core/utils/concurrency";
import { cookie } from "@web/core/browser/cookie";
import { loadJS } from "@web/core/assets";
import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToString } from "@web/core/utils/render";
import { rpc } from '@web/core/network/rpc';
import { session } from "@web/session";
import { sprintf } from "@web/core/utils/strings";
const WebsiteSaleCheckoutSendcloudWidget = publicWidget.registry.WebsiteSaleCheckout;

WebsiteSaleCheckoutSendcloudWidget.include({
    events: Object.assign({
        "click .o_website_sendcloud_btn": "_onClickSendcloudButton",
        "click .o_website_sendcloud_address": "_onClickSendcloudAddress",
    }, WebsiteSaleCheckoutSendcloudWidget.prototype.events),

    init() {
        this._super.apply(this, arguments);
        loadJS("/delivery_sendcloud_oca/static/src/lib/sendcloud/api.min.js");
        this.KeepLast = new KeepLast();
    },
    /**
     * Hide the sendcloud pickup locations.
     *
     * @private
     * @returns {void}
     */
    _hidePickupLocation() {
        this._super(...arguments);
        // eslint-disable-next-line no-undef
        const website_sendcloud_divs = document.querySelectorAll(
            '.o_website_sendcloud_div:not(.d-none)'
        );
        website_sendcloud_divs.forEach(website_sendcloud_div => {
            website_sendcloud_div.classList.add('d-none');
        });
        var $allSendcloudAddr = this.$el.find(".o_website_sendcloud_address");
        $allSendcloudAddr.remove();
    },

    _updateAmountBadge(radio, result) {
        this._super(...arguments);
        const deliveryMethodContainer = this._getDeliveryMethodContainer(radio);
        const pickupLocation = deliveryMethodContainer.querySelector('[name="website_sendcloud_btn"]');
        if (pickupLocation)
        {pickupLocation.dataset.sendcloudDetails = result.sendcloud_details;}
    },
    async _showPickupLocation(radio) {
        await this._super(...arguments);
        if (!radio.dataset.sendcloudServicePointRequired || radio.disabled) {
            return;
        }
        var xpath_to_search = sprintf("input[name='o_delivery_radio']:checked");
        var $carrierSelect = this.$el.find(xpath_to_search).parents(".list-group-item");
        var $sendcloudBtn = $carrierSelect.find("button[name='website_sendcloud_btn']");
        $sendcloudBtn.parent().removeClass('d-none');
    },
    _onClickSendcloudButton: async function(ev) {
        ev.preventDefault();
        var $btn = $(ev.target);
        var sendcloudDetails = $btn.data("sendcloudDetails");
        const availableLanguages = ["en-us", "de-de", "en-gb", "es-es", "fr-fr", "it-it", "nl-nl"];
        const lang = session.bundle_params.lang || cookie.get('frontend_lang') || "en-us";
        const langIndex = lang.replace('_', '-').toLowerCase().indexOf(availableLanguages);
        const selectedLanguage = availableLanguages[langIndex === -1 ? 0 : langIndex];
        const config = {
            apiKey: sendcloudDetails.key,
            country: sendcloudDetails.country_code,
            postalCode: sendcloudDetails.postcode,
            language: selectedLanguage,
            carriers: sendcloudDetails.carrier_name,
        };
        sendcloud.servicePoints.open(
            config,
            this._onServicePointSelected.bind(this, $btn, sendcloudDetails),
            this._onServicePointError.bind(this),
        );
    },

    _onServicePointSelected: function($btn, sendcloudDetails, servicePoint) {

        // Update view
        this.$('.o_website_sendcloud_address').remove();
        var address = renderToString("website_sendcloud_official.Address", {
            servicePoint: servicePoint
        });
        $btn.parent('div').after(address);

        // Update sale order
        this.KeepLast.add(rpc("/shop/sendcloud_update_service_point_address",{
                order_id: sendcloudDetails.order_id,
                sendcloud_service_point_address: JSON.stringify(servicePoint),
        }));

        // Enable pay button
        this._enableMainButton();
    },

    _onServicePointError: function(errors) {
        const irrelevantErrors = ['Closed'];
        var relevantErrors = $(errors).not(irrelevantErrors).get();
        if (relevantErrors.length) {
            // eslint-disable-next-line no-undef
            alert(relevantErrors.join("\n"));// eslint-disable-line no-alert
            return;
        }
    },

    _onClickSendcloudAddress: function(ev) {
        ev.stopPropagation();
    }
});
