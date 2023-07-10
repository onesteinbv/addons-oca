/** @odoo-module **/

import publicWidget from 'web.public.widget';

publicWidget.registry.OpenStreetMap = publicWidget.Widget.extend({
    selector: '.s_openstreetmap',

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
    start: function () {
        if (!this.el.querySelector('.s_openstreetmap_embedded')) {
            const dataset = this.el.dataset;
            if (dataset.mapAddress) {
                this._rpc({
                    method: "geo_find",
                    model: "base.geocoder",
                    args: [dataset.mapAddress],
                }).then((res) => {
                    var url = this.generateOpenStreetMapLink(res, this.el.dataset);
                    if (url) {
                        const objectEl = this.generateOpenStreetMapObject();
                        objectEl.setAttribute('data', url);
                        this.el.querySelector('.s_openstreetmap_color_filter').before(objectEl);
                    }
                });
            }
        }
    },
});

export default publicWidget.registry.OpenStreetMap;
