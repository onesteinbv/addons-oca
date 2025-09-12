import {canPreview, getUrl, showPreview} from "@attachment_preview/js/utils.esm";
import { Component} from "@odoo/owl";
import {SIZES} from "@web/core/ui/ui_service";
import {registry} from "@web/core/registry";
import {sprintf} from "@web/core/utils/strings";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import {useService} from "@web/core/utils/hooks";

class MoveLineAttachmentWidget extends Component {
    static template = "account_move_line_attachment_preview.MoveLineAttachmentWidget";
    static props = standardFieldProps;
    setup() {
        super.setup();
        const ui = useService("ui");
        this.orm = useService("orm");
        // Preview on new tab instead of widget in case the monitor is not big enough
        this.split_screen = ui.size >= SIZES.XXL;
    }

    async openAttachment() {
        var attachment_id = this.props.record.data.preview_attachment_id[0];
        const filename = this.props.record.data.preview_attachment_id[1];
        const split_screen = this.split_screen;
        $(".o_list_renderer").addClass("attachment_preview_list");
        var extension = await this.orm.call(
                "ir.attachment",
                "get_attachment_extension",
                [attachment_id],
            )
            // In case extension not supported, emulate attachment like it's undefined
            if (canPreview(extension)) {
                showPreview(attachment_id, "", extension, filename, split_screen, [
                {
                    id: attachment_id,
                    url: sprintf("/web/content/%s", attachment_id),
                    extension: extension,
                    title: filename,
                    previewUrl: getUrl(
                        attachment_id,
                        sprintf("/web/content/%s#pagemode=none", attachment_id),
                        extension,
                        filename
                    ),
                },
            ]);
            }
    }
}
export const MoveLineAttachmentPreviewWidget = {component: MoveLineAttachmentWidget};
registry.category("fields").add("move_line_attachment_preview_widget", MoveLineAttachmentPreviewWidget);
