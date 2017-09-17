# This is the main loop. It loads/reloads 'song.rb' and calls the 'song'
# function in two separate threads in a loop.

in_thread do
  loop do
    load "<path_to>/song.rb"
    sleep 0.25
  end
end

in_thread do
  puts "restart 'song'"
  loop do
    song
    sleep 0.1
  end
end
