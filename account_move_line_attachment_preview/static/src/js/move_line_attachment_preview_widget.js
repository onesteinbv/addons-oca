/** @odoo-module **/

import {registry} from "@web/core/registry";
import {showPreview, getUrl} from "@attachment_preview/js/utils.esm";
import {sprintf} from "@web/core/utils/strings";
import { useService } from "@web/core/utils/hooks";
import { SIZES } from '@web/core/ui/ui_service';

const {Component} = owl;

class MoveLineAttachmentWidget extends Component {
    setup() {
        super.setup();
        const ui = useService("ui");
        this.split_screen = (ui.size >= SIZES.XXL);
    }

    async openAttachment() {

        const attachment_id = this.props.record.data.preview_attachment_id[0];
        const filename = this.props.record.data.preview_attachment_id[1];
        const extension = "PDF";
        const preview_url = getUrl(
            attachment_id,
            sprintf(
                "/web/static/lib/pdfjs/web/viewer.html?file=/web/content/%s#pagemode=none",
                attachment_id
            ),
            extension,
            filename
        );

        showPreview(
            attachment_id,
            "",
            extension,
            filename,
            this.split_screen,
            [{
                id: attachment_id,
                url: sprintf(
                    "/web/content/%s",
                    attachment_id
                ),
                extension: extension,
                title: filename,
                previewUrl: preview_url,
            }]
        );
    }
}

MoveLineAttachmentWidget.template = "account_move_line_attachment_preview.MoveLineAttachmentWidget";
registry.category("fields").add("move_line_attachment_preview_widget", MoveLineAttachmentWidget);
