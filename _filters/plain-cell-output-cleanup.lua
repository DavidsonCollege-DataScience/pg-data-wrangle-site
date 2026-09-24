-- Runs at pre-quarto AFTER the code-window filter. code-window labels every
-- block that has no language as "default", even when the block has opted out
-- of window chrome. Remove that label from cell output so it renders as plain
-- text with no code styling or copy button.
function Div(div)
  if div.classes:includes('cell-output') then
    return div:walk({
      CodeBlock = function(block)
        if block.attributes['code-window-auto-label'] then
          block.attributes['code-window-auto-label'] = nil
          block.classes = block.classes:filter(function(c) return c ~= 'default' end)
        end
        return block
      end
    })
  end
end
