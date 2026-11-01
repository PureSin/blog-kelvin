# {{ .Title }}

{{ with .Params.author | default site.Params.author }}Author: {{ . }}
{{ end }}{{ if not .Date.IsZero }}Published: {{ .Date.Format "2006-01-02" }}
{{ end }}{{ with .Params.tags }}Tags: {{ delimit . ", " }}
{{ end }}URL: {{ .Permalink }}
{{ with .Description }}
> {{ . }}
{{ end }}
{{ .RawContent }}
