# ClaudeCAD

![Video Demo of Claude Blender Modeling](https://img.youtube.com/vi/Li_4rGMCwnk/0.jpg)](https://www.youtube.com/watch?v=Li_4rGMCwnk)


## Inspiration

3D models are one of the best vehicles for learning about mechanical concepts or engineering history, but they are not always available and they are non-interactive. What if you could inference a 3D model from any technical drawing, watch it in motion, ask questions about its operation, make modifications to parameters, output the result for 3D slicing and 3D printing, etc? Let's make 2D drawings into explorable explanations and real objects.

## What it does
It connects Claude Desktop to a locally hosted Blender MCP server, a local Blender instance, and a newly-developed local MCP server which serves as a technical drawing database and server.

The user can name a historical engineering mechanism or artifact. For example, the Wright Brothers Flyer, a planetary gearbox, etc. Claude then generates a 3D model directly from the 2D technical drawings. The user can modify the model by changing parameters, materials, etc., and can ask for information about the model's mechanism, function, and effects of any modifications.

## How we built it
We started from Claude Desktop and experimented with the generation of different categories of Blender models. The initial vision was architectural visualization. We also explored topographic visualization, but neither of these resulted in models with as high quality as experimental modeling from a technical drawing. We developed the technical drawing MCP server in order to enable a single user request to retrieve and generate a model.

## Challenges we ran into
Generating architectural models from photos resulted in models with gaps. Finding blueprints or floorplans for buildings was more difficult than technical drawings (and many of the latter are already programmatically available via the USPTO MCP server), and having dimensions and isometric views helped guide the model. Pivot time.

We ran into out of date documentation, and needed to re-ask Claude to continue manually due to lengthy outputs. We exhausted free tier requests, upgraded to pro, exhausted those, and were told limits refresh just at the submission deadline. Considered max but too expensive for an afternoon hackathon.

## Accomplishments that we're proud of
Getting this to work while knowing next to nothing about Blender. Which is testament to how powerful Claude is when given access to these MCP servers.

## What we learned
MCP is a very powerful protocol and unlocks a Metcalfe's Law-like NxM model instead of weaker N+M set of LLM to service connection possiblities.

## What's next for ClaudeCAD
Adding prompt templates in the technical drawing MCP server to make common material settings the default, or to use MCP sampling requests to counter-ask the LLM to provide appropriate material settings, animation and background preferences. Prompts templates could also perform modifications like stripping text from the filings from the rendered models, or making that optional. Prompts could also include default history and mechanism explanations in the conversation, along with suggested pedagogical model parameter modifications.

Expansion of the database of technical drawings and connection to the already existing USPTO MCP server to allow single prompt generation of any technical object contained in the US Patent and Trademark Offices technical diagram library and archives.

Connection to YouTube MCP server to allow for uploading of rendered output.

Connection to Slack or Discord MCP servers to passively monitor a channel and send MCP notifications when key words are detected describing inventions or models and automatically creating or linking to them.

## Built With
claude
claudecode
fastmpc
python
uv
