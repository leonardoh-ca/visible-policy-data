const fetch = require("node-fetch");

exports.handler = async function (event) {
  const { data } = JSON.parse(event.body);

  const res = await fetch(
    "https://api.github.com/repos/leonardoh-ca/visible-policy-data/dispatches",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.ASKGOV_GITHUB_TOKEN}`,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        event_type: "update-comments",
        client_payload: {
          data: JSON.stringify(data, null, 2)
        }
      })
    }
  );

  return {
    statusCode: res.ok ? 200 : 500,
    body: JSON.stringify({ ok: res.ok })
  };
};
