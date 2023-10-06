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
        if(!this.is_move_line) return res;

        this.attachmentPreviewWidget = new AttachmentPreviewWidget(this);
        this.attachmentPreviewWidget.on(
            "hidden",
            this,
            this._attachmentPreviewWidgetHidden
        );
        onMounted(() => {
            this.attachmentPreviewWidget.insertAfter($(".o_list_renderer"));
            bus.on("open_attachment_preview", this, this._onAttachmentPreview);
        });
        return res;
    },

    _attachmentPreviewWidgetHidden() {
        if(!this.is_move_line) return;
        $(".o_list_renderer").removeClass("attachment_preview");
    },

    _onAttachmentPreview(attachment_id, attachment_info_list) {
        if(!this.is_move_line) return;
        $(".o_list_renderer").addClass("attachment_preview");
        if (attachment_id === undefined) {
            this.attachmentPreviewWidget.$iframe.attr("src", "about:blank");
            $("button.attachment_preview_popout").addClass("d-none");
        } else {
            this.attachmentPreviewWidget.setAttachments(
                attachment_info_list,
                attachment_id
            );
            $("button.attachment_preview_popout").removeClass("d-none");
            this.attachmentPreviewWidget.show();
            window.dispatchEvent(new Event('resize'));
        }
    },
});
