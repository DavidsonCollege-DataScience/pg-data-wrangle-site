-- Keep executed cell output (printed values, messages, warnings) out of code
-- windows. Runs at pre-quarto BEFORE the code-window filter and opts each
-- output block out of window chrome. plain-cell-output-cleanup.lua runs after
-- code-window to finish the job.
function Div(div)
  if div.classes:includes('cell-output') then
    return div:walk({
      CodeBlock = function(block)
        block.attributes['code-window-enabled'] = 'false'
        return block
      end
    })
  end
end
