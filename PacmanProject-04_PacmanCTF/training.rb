10000.times do |i|
  puts "Iterated #{i * 10} time(s)"
  puts `pypy capture.py -r 00_myTeam -q -n 10`
end
