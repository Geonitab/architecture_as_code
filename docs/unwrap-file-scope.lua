-- With file-scope Pandoc wraps every chapter file in <div id="NN_name.md"> so that links to the
-- file resolve. A wrapper keeps the chapter's sections from being top-level blocks, so the EPUB
-- writer no longer splits the book into one file per chapter and writes table-of-contents links
-- without a file name. This filter removes the wrapper and moves its identifier to an empty
-- anchor inside the first heading, so links to the file still resolve and the sections are
-- top-level again. Raw blocks in front of the first heading (for example an HTML comment) stay
-- in front of it.
function Pandoc(doc)
  local out = pandoc.List()
  for _, blk in ipairs(doc.blocks) do
    local first = nil
    if blk.t == 'Div' and blk.identifier:match('%.md$') then
      for i, inner in ipairs(blk.content) do
        if inner.t == 'Header' then first = i; break end
        if inner.t ~= 'RawBlock' then break end
      end
    end
    if first then
      for i = 1, first do out:insert(blk.content[i]) end
      out:insert(pandoc.Div({}, pandoc.Attr(blk.identifier)))
      for i = first + 1, #blk.content do out:insert(blk.content[i]) end
    else
      out:insert(blk)
    end
  end
  doc.blocks = out
  return doc
end
