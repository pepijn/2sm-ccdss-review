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

def extract
  `chmod 600 sources/*.org`
  puts `python extract.py sources/*.pdf`
  `chmod 400 sources/*.org`
end

guard :shell do
  watch(%r{.+\.tex\.gpg}) do |path, _|
    `chmod 600 *.tex`
    `gpg --yes --decrypt-files *.tex.gpg;`
    `bibtex bachelor_thesis.tex`
    `pdflatex bachelor_thesis.tex`
    `pdflatex bachelor_thesis.tex`
    `rm *.tex`
  end

  watch(%r{articles/(.*\.pdf)}) do |path, filename|
    path = Pathname path
    next unless path.exist?
    puts path
    `mv "#{path}" sources`
    extract
    system 'python summarize.py sources/*.org'
  end

  watch('summarize.py') do
    system 'python summarize.py sources/*.org'
  end

  watch('extract.py') do
    extract
  end

  watch('save.py') do
    `python save.py output.org`
  end

  watch('extract2.py') do
    `python extract2.py "articles2/Dexter\ et\ al.\ -\ 2001\ -\ A\ Computerized\ Reminder\ System\ to\ Increase\ the\ Use\ of\ Preventive\ Care\ for\ Hospitalized\ Patients.pdf" < saved.yml`
  end
end
