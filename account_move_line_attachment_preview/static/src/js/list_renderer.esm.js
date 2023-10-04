/** @odoo-module **/
import {onMounted} from "@odoo/owl";
import {AttachmentPreviewWidget} from "@attachment_preview/js/attachmentPreviewWidget.esm";
import {ListRenderer} from "@web/views/list/list_renderer";
import {bus} from "web.core";
import {patch} from "@web/core/utils/patch";

patch(ListRenderer.prototype, "account_move_line_attachment_preview.ListRenderer", {
    attachmentPreviewWidget: null,

    setup() {
        var res = this._super(...arguments);
        this.is_move_line = this.props.list.resModel === "account.move.line";
        this.attachmentPreviewWidget = new AttachmentPreviewWidget(this);
        this.attachmentPreviewWidget.on(
            "hidden",
            this,
            this._attachmentPreviewWidgetHidden
        );
        onMounted(() => {
            if (this.is_move_line) {
                this.attachmentPreviewWidget.insertAfter($(".o_list_renderer"));
                bus.on("open_attachment_preview", this, this._onAttachmentPreview);
            }
        });
        return res;
    },

    _attachmentPreviewWidgetHidden() {
        if (this.is_move_line) {
            $(".o_list_renderer").removeClass("attachment_preview");
        }
    },

    _onAttachmentPreview(attachment_id, attachment_info_list) {
        if (this.is_move_line) {
            $(".o_list_renderer").addClass("attachment_preview");
            this.attachmentPreviewWidget.setAttachments(
                attachment_info_list,
                attachment_id
            );
            this.attachmentPreviewWidget.show();
            window.dispatchEvent(new Event('resize'));
        }
    },
});
