/** @odoo-module **/

import {_t} from 'web.core';
import options from 'web_editor.snippets.options';

options.registry.OpenStreetMap = options.Class.extend({

    // --------------------------------------------------------------------------
    // Utility Functions
    // --------------------------------------------------------------------------

    generateOpenStreetMapObject: function() {
        const objectEl = document.createElement('object');
        objectEl.classList.add('s_openstreetmap_embedded', 'o_not_editable');
        objectEl.setAttribute('width', '100%');
        objectEl.setAttribute('height', '100%');
        objectEl.setAttribute('frameborder', '0');
        objectEl.setAttribute('scrolling', 'no');
        objectEl.setAttribute('marginheight', '0');
        objectEl.setAttribute('marginwidth', '0');
        objectEl.setAttribute('data', '');
        return objectEl;
    },

    generateOpenStreetMapLink: function(coordinates, dataset) {
        if (coordinates) {
            var earthRadius = 6378137;

            var area = parseFloat(dataset.mapZoom);
            var offset = area / 2;

            var minlon =
                coordinates[1] +
                (-offset / (earthRadius * Math.cos((Math.PI * coordinates[0]) / 180))) *
                    (180 / Math.PI);
            var minlat = coordinates[0] + (-offset / earthRadius) * (180 / Math.PI);
            var maxlon =
                coordinates[1] +
                (offset / (earthRadius * Math.cos((Math.PI * coordinates[0]) / 180))) *
                    (180 / Math.PI);
            var maxlat = coordinates[0] + (offset / earthRadius) * (180 / Math.PI);

            const url =
                "https://www.openstreetmap.org/export/embed.html?bbox=" +
                encodeURIComponent(
                    minlon + "," + minlat + "," + maxlon + "," + maxlat
                ) +
                "&marker=" +
                encodeURIComponent(coordinates[0] + "," + coordinates[1]) +
                "&layer=" +
                dataset.mapType;

            return url;
        }
        return "";
    },

    /**
     * @override
     */
    onBuilt() {
        const objectEl = this.generateOpenStreetMapObject();
        this.$target[0].querySelector('.s_openstreetmap_color_filter').before(objectEl);
        this._updateSource();
    },

    // --------------------------------------------------------------------------
    // Options
    // --------------------------------------------------------------------------

    /**
     * @see this.selectClass for parameters
     */
    /* eslint-disable no-unused-vars */
    async selectDataAttribute(previewMode, widgetValue, params) {
        await this._super(...arguments);
        if (['mapAddress', 'mapType', 'mapZoom'].includes(params.attributeName)) {
            this._updateSource();
        }
    },

    /**
     * @see this.selectClass for parameters
     */
    /* eslint-disable no-unused-vars */
    async showDescription(previewMode, widgetValue, params) {
        const descriptionEl = this.$target[0].querySelector('.description');
        if (widgetValue && !descriptionEl) {
            this.$target.append($(`
                <div class="description">
                    <font>${_t('Visit us:')}</font>
                    <span>${_t('Our office is open Monday – Friday 8:30 a.m. – 4:00 p.m.')}</span>
                </div>`)
            );
        } else if (!widgetValue && descriptionEl) {
            descriptionEl.remove();
        }
    },

    // --------------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------------

    /**
     * @override
     */
    /* eslint-disable no-unused-vars */
    _computeWidgetState(methodName, params) {
        if (methodName === 'showDescription') {
            return Boolean(this.$target[0].querySelector('.description'));
        }
        return this._super(...arguments);
    },

    /**
     * @private
     */
    _updateSource() {
        const dataset = this.$target[0].dataset;
        const $embedded = this.$target.find(".s_openstreetmap_embedded");
        const $info = this.$target.find(".missing_option_warning");
        if (dataset.mapAddress) {
            this._rpc({
                method: "geo_find",
                model: "base.geocoder",
                args: [dataset.mapAddress],
            }).then((res) => {
                var url = this.generateOpenStreetMapLink(res, dataset);
                if (url) {
                    if (url !== $embedded.attr("data")) {
                        $embedded.attr("data", url);
                    }
                    $embedded.removeClass("d-none");
                    $info.addClass("d-none");
                } else {
                    $embedded.attr("data", "");
                    $embedded.addClass("d-none");
                    $info.removeClass("d-none");
                }
            });
        } else {
            $embedded.attr("data", "");
            $embedded.addClass("d-none");
            $info.removeClass("d-none");
        }
    },
});

export default {
    OpenStreetMap: options.registry.OpenStreetMap,
};
