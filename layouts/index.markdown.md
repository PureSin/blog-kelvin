# {{ site.Title }}

{{ site.Params.description }}

Author: {{ site.Params.author }} · [About]({{ "about/" | absURL }}) · [All posts]({{ "posts/" | absURL }}) · [RSS]({{ "index.xml" | absURL }}) · [llms.txt]({{ "llms.txt" | absURL }})

## Recent posts
{{ range where site.RegularPages "Type" "posts" }}
- [{{ .Title }}]({{ .Permalink }}) ({{ .Date.Format "2006-01-02" }}){{ with .Description }}: {{ . }}{{ end }}
{{- end }}

## Elsewhere
{{ range sort site.Params.social "weight" }}
- [{{ .name }}]({{ .url }})
{{- end }}
