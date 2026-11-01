# {{ .Title }} · {{ site.Title }}

URL: {{ .Permalink }}
{{ with .Content }}
{{ $.RawContent }}
{{ end }}
{{ range .Pages }}- [{{ .Title }}]({{ .Permalink }}){{ if not .Date.IsZero }} ({{ .Date.Format "2006-01-02" }}){{ end }}{{ with .Description }}: {{ . }}{{ end }}
{{ end }}
