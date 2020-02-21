## Travis tests were successful
Hey @{{pullRequestAuthor}},
 no major flaws where found with your code. Still you might want to look at this logfile, as some optional improvements might be suggested.

{{#jobs}}
### {{displayName}}
{{#scripts}}
<details>
  <summary>
    <strong>
     {{command}}
    </strong>
  </summary>

```
{{&contents}}
```
</details>
<br />
{{/scripts}}
{{/jobs}}
