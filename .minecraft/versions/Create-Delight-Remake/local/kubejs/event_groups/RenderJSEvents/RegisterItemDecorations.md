# RenderJSEvents.RegisterItemDecorations

## Basic info

- Valid script types: [CLIENT]

- Has result? ✘

- Event class: ItemDecorationsRegisterEvent (third-party)

### Available fields:

| Name | Type | Static? |
| ---- | ---- | ------- |

Note: Even if no fields are listed above, some methods are still available as fields through *beans*.

### Available methods:

| Name | Parameters | Return type | Static? |
| ---- | ---------- | ----------- | ------- |
| register | Item, Consumer<RenderContext> |  | void | ✘ |
| register | Item, String, Consumer<RenderContext> |  | void | ✘ |
| registerForAllItem | Consumer<RenderContext> |  | void | ✘ |
| registerForAllItem | String, Consumer<RenderContext> |  | void | ✘ |
| exit | Object |  | Object | ✘ |
| exit |  |  | Object | ✘ |
| success | Object |  | Object | ✘ |
| success |  |  | Object | ✘ |
| cancel | Object |  | Object | ✘ |
| cancel |  |  | Object | ✘ |


### Documented members:

- `void register(Item var0, Consumer<RenderContext> var1)`

  Parameters:
  - var0: Item
  - var1: Consumer<RenderContext>

```
Register an ItemDecorator, and if it has already been registered, return the previously registered ItemDecorator. 
When reloading, the new content will be automatically updated to the corresponding ItemDecorator
```

- `void register(Item var0, String var1, Consumer<RenderContext> var2)`

  Parameters:
  - var0: Item
  - var1: String
  - var2: Consumer<RenderContext>

```
don't use this,This method will be removed in the future
```

- `void registerForAllItem(Consumer<RenderContext> var0)`

  Parameters:
  - var0: Consumer<RenderContext>

```
Register an ItemDecorator for all items
```

- `void registerForAllItem(String var0, Consumer<RenderContext> var1)`

  Parameters:
  - var0: String
  - var1: Consumer<RenderContext>

```
don't use this,This method will be removed in the future
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
RenderJSEvents.RegisterItemDecorations((event) => {
	// This space (un)intentionally left blank
});
```

