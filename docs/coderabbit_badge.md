# CodeRabbit Pull Request Reviews Badge

This badge shows the number of pull requests reviewed by [CodeRabbit](https://coderabbit.ai).

## Path Parameters

| Parameter | Required | Options | Description |
|-----------|---------|---------|-------------|
| `provider` | **Yes** | `github`, `bitbucket`, `gitlab` | Version control provider |
| `org` | **Yes** | string | Organization or user name |
| `repo` | **Yes** | string | Repository name |

## Query Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| `style` | `flat`, `flat-square`, `plastic`, `for-the-badge`, `social` | Badge style (default `flat`) |
| `logo` | icon slug from [Simple Icons](https://github.com/simple-icons/simple-icons) | Optional logo |
| `logoColor` | color value | Color of the logo |
| `logoSize` | `auto` or size string | Adaptive logo size |
| `label` | string | Override left-hand text |
| `labelColor` | color value | Left part background color |
| `color` | color value | Right part background color |
| `cacheSeconds` | string | HTTP cache lifetime |
| `link` | `string[]` | URLs to open when badge is clicked |

Use these parameters to customize the badge URL in your README or documentation.
