Visual Style Test App
=====================

The visual style test app lets you preview the site wide styling
for a collection of common widgets and components. Out of the box,
only bootstrap is included, but other apps can also register their
own widgets to be displayed.


Installation
------------

0. Add `visual_style` to `INSTALLED_APPS`
0. In your application or site-wide templates directory, add a template
   named `visual_style/base.html`. This template must contain the stylesheets
   and javascript that are common to all pages on the site, and sufficient to
   display the registered components. In most cases, you can get away with the
   following template:
```html
{% extends "site_base.html" %}
```
0. Include `visual_style.urls` in your urlconf.


Registering Components
----------------------

If you have any components that are in use site-wide, you can create a template
called `visual_style/snippets/<component-name>.html` in the application defining
the component. The component will automatically be added to the visual style
test page.
