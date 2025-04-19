// netlify/functions/write-comment.js
const { Octokit } = require("@octokit/rest");

exports.handler = async (event) => {
  const body = JSON.parse(event.body || "{}");
  const token = process.env.ASKGOV_GITHUB_TOKEN;
  const owner = "leonardoh-ca";
  const repo = "visible-policy-data";
  const path = "comments.json";

  const octokit = new Octokit({ auth: token });

  try {
    const { data: existingFile } = await octokit.repos.getContent({
      owner,
      repo,
      path,
    });

    const res = await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path,
      message: `📝 Update comments.json`,
      content: Buffer.from(body.data).toString("base64"),
      sha: existingFile.sha,
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ success: true, url: res.data.content.html_url }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};
