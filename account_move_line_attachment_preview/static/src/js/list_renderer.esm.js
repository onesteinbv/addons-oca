import {AttachmentPreviewWidget} from "@attachment_preview/js/attachmentPreviewWidget.esm";
import {ListRenderer} from "@web/views/list/list_renderer";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";

export class AttachmentPreviewListRenderer extends ListRenderer {
    static template = "account_move_line_attachment_preview.ListRenderer";

    static components = {
        ...ListRenderer.components,
        AttachmentPreviewWidget
    };
};

export const AttachmentPreviewListView = {
    ...listView,
    Renderer: AttachmentPreviewListRenderer,
};

registry.category("views").add("attachment_preview_list_view", AttachmentPreviewListView);
