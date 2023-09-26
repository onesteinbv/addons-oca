/** @odoo-module **/

import {attr, many} from "@mail/model/model_field";
import {registerPatch} from "@mail/model/model_core";

registerPatch({
    name: "MessageListView",
    recordMethods: {
        toggleMessageFailedBoxVisibility() {
            this.update({
                isMessageFailedBoxVisible: !this.isMessageFailedBoxVisible,
            });
        },
    },
    fields: {
        isMessageFailedBoxVisible: attr({
            default: true,
        }),
        messageFailedListViewItems: many("MessageListViewItem", {
            compute() {
                return this.messageListViewItems.filter(
                    (messageListViewItem) => messageListViewItem.isFailedChatterMessage
                );
            },
        }),
    },
});
