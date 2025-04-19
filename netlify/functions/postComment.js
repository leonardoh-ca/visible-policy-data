// /netlify/functions/postComment.js
const { Octokit } = require("@octokit/rest");

exports.handler = async function (event, context) {
  const token = process.env.ASKGOV_GITHUB_TOKEN;
  const repo = "visible-policy-data"; // 你的 repo 名字
  const owner = "leonardoh-ca";       // 你的用户名
  const filePath = "comments.json";

  const octokit = new Octokit({ auth: token });

  try {
    const { name, district, message, timestamp } = JSON.parse(event.body);

    // 1. 读取原始 comments.json
    const { data: file } = await octokit.repos.getContent({ owner, repo, path: filePath });
    const content = Buffer.from(file.content, "base64").toString();
    const json = JSON.parse(content);

    // 2. 添加新留言
    json.push({ name, district, message, timestamp });

    // 3. 写回 GitHub
    const newContent = Buffer.from(JSON.stringify(json, null, 2)).toString("base64");
    await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path: filePath,
      message: "💬 New AskGov Comment",
      content: newContent,
      sha: file.sha,
    });

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (err) {
    console.error("❌ Error writing comment:", err);
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
