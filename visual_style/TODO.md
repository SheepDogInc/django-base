TODO
====

- Add a way to register more complex components if necessary (ex. views
  containing sheepdog tables or the like.)
- Respect the template loaders setting when finding templates.
- Only allow admins to see the visual style test page in debug mode.
- Extract headers bottom-up instead of top-down to remove special casing
  of h1 / h2 handling. (ie. run through the element list backwards, and decide to
  include a header based on the last item handled before the header - if it was at
  a lower level, include it, otherwise do not.)
