from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# 新建一个 forward
class SlackForward:
    def __init__(self, slack_token, channel):
        self.slack_client = WebClient(token=slack_token)
        self.channel = channel

    def forward(self, message):
        self.slack_client.api_call(
            "chat.postMessage", channel=self.channel, text=message
        )

    def send_image(self, image_path):
        """
        将截图发送到 Slack 频道。

        Parameters:
            - image_path: str, 截图文件的路径。
        """
        # 将截图发送到 Slack 频道

        # conversations_list = client.conversations_list()
        # # 遍历响应中的频道信息
        # for channel in conversations_list["channels"]:
        #     channel_id = channel["id"]
        #     channel_name = channel["name"]
        #     channel_is_private = channel["is_private"]

        #     # 打印频道信息
        #     print(
        #         f"Channel ID: {channel_id}, Name: {channel_name}, Private: {channel_is_private}"
        #     )

        try:
            response = self.slack_client.files_upload_v2(
                channel=self.channel,  # 替换为你的频道 ID
                # channel=self.slack_channel,
                file=image_path,
                initial_comment="Difference detected!",
            )
            print("File uploaded successfully:", response["file"]["name"])
        except SlackApiError as e:
            print(f"Error uploading file to Slack: {e.response['error']}")
