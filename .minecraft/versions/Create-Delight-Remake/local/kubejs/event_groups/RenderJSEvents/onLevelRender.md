# RenderJSEvents.onLevelRender

## Basic info

- Valid script types: [CLIENT]

- Has result? ✘

- Event class: RenderJSRenderLevelEvent (third-party)

### Available fields:

| Name | Type | Static? |
| ---- | ---- | ------- |

Note: Even if no fields are listed above, some methods are still available as fields through *beans*.

### Available methods:

| Name | Parameters | Return type | Static? |
| ---- | ---------- | ----------- | ------- |
| getEvent |  |  | RenderLevelStageEvent | ✘ |
| getPoseStack |  |  | PoseStack | ✘ |
| getGuiGraphics |  |  | GuiGraphics | ✘ |
| getFrustum |  |  | Frustum | ✘ |
| getRenderTick |  |  | int | ✘ |
| getLevelRenderer |  |  | LevelRenderer | ✘ |
| getPartialTick |  |  | float | ✘ |
| getStage |  |  | Stage | ✘ |
| getProjectionMatrix |  |  | Matrix4f | ✘ |
| getCamera |  |  | Camera | ✘ |
| setColor | int, int, int, int |  | void | ✘ |
| getColor |  |  | int[] | ✘ |
| setBlockRenderType | RenderType |  | void | ✘ |
| packLight | Level, BlockPos |  | int | ✘ |
| renderHitOutline | BlockState, PoseStack |  | void | ✘ |
| renderHitOutline | BlockState, PoseStack, MultiBufferSource, Entity, BlockPos |  | void | ✘ |
| renderHitOutline | BlockState, PoseStack, MultiBufferSource |  | void | ✘ |
| renderHitOutline | BlockState, PoseStack, MultiBufferSource, Entity |  | void | ✘ |
| getBlockRenderType |  |  | RenderType | ✘ |
| getBufferSource |  |  | MultiBufferSource$BufferSource | ✘ |
| transformerCamera | PoseStack, Camera |  | void | ✘ |
| renderLevelItem | ItemStack, PoseStack, MultiBufferSource, int |  | void | ✘ |
| renderLevelItem | ItemStack, PoseStack |  | void | ✘ |
| renderLevelItem | ItemStack, PoseStack, MultiBufferSource, int, int |  | void | ✘ |
| renderLevelItem | ItemStack, PoseStack, MultiBufferSource |  | void | ✘ |
| restColor |  |  | void | ✘ |
| renderSingleBlock | BlockState, PoseStack, MultiBufferSource |  | void | ✘ |
| renderSingleBlock | BlockState, PoseStack, MultiBufferSource, int, int, ModelData, RenderType |  | void | ✘ |
| renderSingleBlock | BlockState, PoseStack, MultiBufferSource, int, int, ModelData |  | void | ✘ |
| renderSingleBlock | BlockState, PoseStack |  | void | ✘ |
| renderSingleBlock | BlockState, PoseStack, MultiBufferSource, int |  | void | ✘ |
| renderSingleBlock | BlockState, PoseStack, MultiBufferSource, int, int |  | void | ✘ |
| restBlockRenderType |  |  | void | ✘ |
| setTranslucentBlockRenderType |  |  | void | ✘ |
| transformerToBlockPose | PoseStack, BlockPos |  | void | ✘ |
| fill | int, int, int, int, int |  | void | ✘ |
| fill | int, int, int, int, int, int, int, int |  | void | ✘ |
| drawString | Component, int, int, int, int, int, int |  | void | ✘ |
| drawString | Component, int, int, int |  | void | ✘ |
| drawTexture | ResourceLocation, int, int, int, int |  | void | ✘ |
| drawTexture | ResourceLocation, int, int, int, int, int, int, int, int, int |  | void | ✘ |
| drawTexture | ResourceLocation, int, int, int, int, int, int, int, int |  | void | ✘ |
| renderGuiItem | ItemStack, int, int |  | void | ✘ |
| drawShadowString | Component, int, int, int, int, int, int |  | void | ✘ |
| drawShadowString | Component, int, int, int |  | void | ✘ |
| vLine | PoseStack, int, int, int, int |  | void | ✘ |
| vLine | int, int, int, int, int, int, int |  | void | ✘ |
| hLine | int, int, int, int, int, int, int |  | void | ✘ |
| hLine | int, int, int, int |  | void | ✘ |
| scale | float, float, float |  | void | ✘ |
| scale | float, float |  | void | ✘ |
| translate | float, float, float |  | void | ✘ |
| translate | float, float |  | void | ✘ |
| pushPose |  |  | void | ✘ |
| mulPose | Quaternionf |  | void | ✘ |
| rotationDegreesZ | float |  | void | ✘ |
| rotationDegreesX | float |  | void | ✘ |
| popPose |  |  | void | ✘ |
| rotationDegreesY | float |  | void | ✘ |
| getEntity |  |  | Entity | ✘ |
| getPlayer |  |  | LocalPlayer | ✘ |
| removeGameStage | String |  | void | ✘ |
| addGameStage | String |  | void | ✘ |
| hasGameStage | String |  | boolean | ✘ |
| getLevel |  |  | Level | ✘ |
| getServer |  |  | MinecraftServer | ✘ |
| exit | Object |  | Object | ✘ |
| exit |  |  | Object | ✘ |
| success | Object |  | Object | ✘ |
| success |  |  | Object | ✘ |
| cancel | Object |  | Object | ✘ |
| cancel |  |  | Object | ✘ |


### Documented members:

- `void setTranslucentBlockRenderType()`
```
If you want to make the block semi transparent, please use this first,and set rgba
```

- `void renderGuiItem(ItemStack var0, int var1, int var2)`

  Parameters:
  - var0: ItemStack
  - var1: int
  - var2: int

```
don's use this in level render, use renderLevelItem
```

- `void removeGameStage(String var0)`

  Parameters:
  - var0: String

```
Removes the specified game stage from the player
```

- `void addGameStage(String var0)`

  Parameters:
  - var0: String

```
Adds the specified game stage to the player
```

- `boolean hasGameStage(String var0)`

  Parameters:
  - var0: String

```
Checks if the player has the specified game stage
```

- `Object exit(Object var0)`

  Parameters:
  - var0: Object

```
Stops the event with the given exit value. Execution will be stopped **immediately**.

`exit` denotes a `default` outcome.
```

- `Object exit()`
```
Stops the event with default exit value. Execution will be stopped **immediately**.

`exit` denotes a `default` outcome.
```

- `Object success(Object var0)`

  Parameters:
  - var0: Object

```
Stops the event with the given exit value. Execution will be stopped **immediately**.

`success` denotes a `true` outcome.
```

- `Object success()`
```
Stops the event with default exit value. Execution will be stopped **immediately**.

`success` denotes a `true` outcome.
```

- `Object cancel(Object var0)`

  Parameters:
  - var0: Object

```
Cancels the event with the given exit value. Execution will be stopped **immediately**.

`cancel` denotes a `false` outcome.
```

- `Object cancel()`
```
Cancels the event with default exit value. Execution will be stopped **immediately**.

`cancel` denotes a `false` outcome.
```



### Example script:

```js
RenderJSEvents.onLevelRender((event) => {
	// This space (un)intentionally left blank
});
```

