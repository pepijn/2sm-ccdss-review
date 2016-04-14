# A sample Guardfile
# More info at https://github.com/guard/guard#readme

## Uncomment and set this to only include directories you want to watch
# directories %w(app lib config test spec features) \
#  .select{|d| Dir.exists?(d) ? d : UI.warning("Directory #{d} does not exist")}

## Note: if you are using the `directories` clause above and you are not
## watching the project directory ('.'), then you will want to move
## the Guardfile to a watched dir and symlink it back, e.g.
#
#  $ mkdir config
#  $ mv Guardfile config/
#  $ ln -s config/Guardfile .
#
# and, you'll have to watch "config/Guardfile" instead of "Guardfile"


# Add files and commands to this file, like the example:
#   watch(%r{file/path}) { `command(s)` }
#
guard :shell do
  watch('bachelor_thesis.tex.gpg') do |path, _|
    decrypted = path[0..-5]
    `chmod 600 #{decrypted}`
    `gpg --batch --yes --output #{decrypted} --decrypt #{path}`
    `chmod 400 #{decrypted}`
    `bibtex #{decrypted}`
    `pdflatex #{decrypted}`
    `pdflatex #{decrypted}`
  end

  watch(%r{sources/(.*).pdf}) do |path, _|
    puts path
    `chmod 600 sources/*.org`
    `python extract.py sources/*.pdf`
    `rm "#{path}"`
    `chmod 400 sources/*.org`
  end
end
