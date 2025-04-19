const { Octokit } = require("@octokit/rest");
const fetch = require("node-fetch");

exports.handler = async function (event) {
  const { data } = JSON.parse(event.body);

  const GITHUB_TOKEN = process.env.ASKGOV_GITHUB_TOKEN;
  const octokit = new Octokit({ auth: GITHUB_TOKEN });

  const owner = "leonardoh-ca";
  const repo = "visible-policy-data";
  const path = "comments.json";

  try {
    // 1. 获取文件 SHA 和内容
    const { data: fileData } = await octokit.repos.getContent({ owner, repo, path });
    const sha = fileData.sha;
    let existing = JSON.parse(Buffer.from(fileData.content, 'base64').toString());

    // 2. 更新内容
    existing = Array.isArray(existing) ? data : [];
    const newContent = Buffer.from(JSON.stringify(data, null, 2)).toString("base64");

    // 3. 提交变更
    await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path,
      message: "🗳️ New AskGov Comment",
      content: newContent,
      sha
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ message: "Updated comments.json" })
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
};
