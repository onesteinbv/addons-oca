import {onWillStart,useEffect} from "@odoo/owl";
import {
    WebsiteLoader,
} from "@website/components/website_loader/website_loader";
import {patch} from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(WebsiteLoader.prototype, {
    setup() {
        super.setup();
        this.orm = useService('orm');
        onWillStart(async () => {
            this.website_logo_url = await this.orm.call('website', 'get_website_logo_url')
        });
        useEffect(
            (isVisible) => {
                if (isVisible) {
                    // eslint-disable-next-line no-undef
                    var htmlTag = document.getElementsByClassName("o_website_loader_odoo_logo");
                    htmlTag[0].style.setProperty('--configurator-logo',this.website_logo_url);
                }
            },
            () => [this.state.isVisible]
        );
    },
});
