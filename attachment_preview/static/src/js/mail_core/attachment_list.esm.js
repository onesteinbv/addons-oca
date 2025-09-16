import {canPreview, getUrl, showPreview} from "../utils.esm";
import {AttachmentList} from "@mail/core/common/attachment_list";
import {onWillStart} from "@odoo/owl";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";

patch(AttachmentList.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        onWillStart(async () => {
            var attachments = Object(
                this.props.attachments.map((attachment) => {
                    if (
                        attachment.defaultSource &&
                        attachment.defaultSource.length > 38
                    ) {
                        return {
                            id: attachment.id,
                            url: attachment.defaultSource,
                            extension: attachment.extension,
                            title: attachment.name,
                        };
                    }
                    return {
                        id: attachment.id,
                        url: "/web/content?id=" + attachment.id + "&download=true",
                        extension: attachment.extension,
                        title: attachment.name,
                    };
                })
            );
            var attachment_ids = [];
            for (const i in attachments) {
                attachment_ids.push(attachments[i].id);
            }
            var extensions = await this.orm.call(
                "ir.attachment",
                "get_attachment_extension",
                [attachment_ids]
            );
            var previewableAttachments = [];
            var previewableAttachmentIds = [];
            for (const i in attachments) {
                const attachment = attachments[i];
                if (canPreview(extensions[attachment.id])) {
                    previewableAttachmentIds.push(attachment.id);
                    previewableAttachments.push({
                        id: attachment.id,
                        url: attachment.url,
                        extension: extensions[attachment.id],
                        title: attachment.title,
                        previewUrl: getUrl(
                            attachment.id,
                            attachment.url,
                            extensions[attachment.id],
                            attachment.title
                        ),
                    });
                }
            }
            this.previewableAttachments = previewableAttachments;
            this.previewableAttachmentIds = previewableAttachmentIds;
        });
    },

    _onPreviewAttachment(attachment) {
        // eslint-disable-next-line no-undef
        var $target = $(event.currentTarget);
        var split_screen = $target.attr("data-target") !== "new";
        var current_attachment = this.previewableAttachments.filter(
            (attachment_rec) => attachment_rec.id === attachment.id
        );
        var extension = false;
        if (current_attachment.length === 0) {
            extension = attachment.extension;
        } else {
            extension = current_attachment[0].extension;
        }
        showPreview(
            attachment.id,
            attachment.defaultSource,
            extension,
            attachment.filename,
            split_screen,
            this.previewableAttachments
        );
    },

    _canPreviewAttachment(attachment) {
        return this.previewableAttachmentIds.includes(attachment.id);
    },
});
