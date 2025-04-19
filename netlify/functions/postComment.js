const { Octokit } = require("@octokit/core");

exports.handler = async function(event) {
  const token = process.env.ASKGOV_GITHUB_TOKEN;
  const octokit = new Octokit({ auth: token });

  const owner = "leonardoh-ca";
  const repo = "visible-policy-data";
  const path = "comments.json";

  const body = JSON.parse(event.body || "{}");
  const newContent = body.data;

  try {
    const { data: { sha } } = await octokit.request("GET /repos/{owner}/{repo}/contents/{path}", {
      owner,
      repo,
      path
    });

    await octokit.request("PUT /repos/{owner}/{repo}/contents/{path}", {
      owner,
      repo,
      path,
      message: "Update comments.json via AskGov",
      content: Buffer.from(newContent).toString("base64"),
      sha
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ success: true })
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message })
    };
  }
};
