import {
    Configurator,DescriptionScreen,FeaturesSelectionScreen,PaletteSelectionScreen,ThemeSelectionScreen,WelcomeScreen
} from "@website/client_actions/configurator/configurator";
import {onMounted,onWillStart} from "@odoo/owl";
import {patch} from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(Configurator.prototype, {
    setup() {
        super.setup();
        onMounted(this.onMounted);
        onWillStart(async () => {
            this.website_logo_url = await this.orm.call('website', 'get_website_logo_url')
        })
    },
    async onMounted() {
        // eslint-disable-next-line no-undef
        var htmlTag = document.getElementsByClassName("o_configurator_odoo_logo");
        htmlTag[0].style.setProperty('--configurator-logo',this.website_logo_url);
    }

});

patch(WelcomeScreen.prototype, {
    setup() {
        super.setup();
        onMounted(this.onMounted);
        this.orm = useService('orm');
        onWillStart(async () => {
            this.website_logo_url = await this.orm.call('website', 'get_website_logo_url')
        })
    },
    onMounted() {
        // eslint-disable-next-line no-undef
        var htmlTag = document.getElementsByClassName("o_configurator_odoo_logo");
        htmlTag[0].style.setProperty('--configurator-logo',this.website_logo_url);
    }
});

patch(DescriptionScreen.prototype, {
    setup() {
        super.setup();
        onWillStart(async () => {
            this.website_logo_url = await this.orm.call('website', 'get_website_logo_url')
        })
    },
    onMounted() {
        // eslint-disable-next-line no-undef
        var htmlTag = document.getElementsByClassName("o_configurator_odoo_logo");
        htmlTag[0].style.setProperty('--configurator-logo',this.website_logo_url);
        super.onMounted();
    }
});

patch(PaletteSelectionScreen.prototype, {
    setup() {
        super.setup();
        onMounted(this.onMounted);
        onWillStart(async () => {
            this.website_logo_url = await this.orm.call('website', 'get_website_logo_url')
        })
    },
    onMounted() {
        // eslint-disable-next-line no-undef
        var htmlTag = document.getElementsByClassName("o_configurator_odoo_logo");
        htmlTag[0].style.setProperty('--configurator-logo',this.website_logo_url);
    }
});

patch(FeaturesSelectionScreen.prototype, {
    setup() {
        super.setup();
        onMounted(this.onMounted);
        onWillStart(async () => {
            this.website_logo_url = await this.orm.call('website', 'get_website_logo_url')
        })
    },
    onMounted() {
        // eslint-disable-next-line no-undef
        var htmlTag = document.getElementsByClassName("o_configurator_odoo_logo");
        htmlTag[0].style.setProperty('--configurator-logo',this.website_logo_url);
    }
});

patch(ThemeSelectionScreen.prototype, {
    setup() {
        super.setup();
        onMounted(this.onMounted);
        onWillStart(async () => {
            this.website_logo_url = await this.orm.call('website', 'get_website_logo_url')
        })
    },
    onMounted() {
        // eslint-disable-next-line no-undef
        var htmlTag = document.getElementsByClassName("o_configurator_odoo_logo");
        htmlTag[0].style.setProperty('--configurator-logo',this.website_logo_url);
    }
});
