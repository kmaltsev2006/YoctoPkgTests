#include <boost/filesystem.hpp>
#include <boost/thread.hpp>
#include <boost/chrono.hpp>
#include <boost/atomic.hpp>
#include <boost/system/error_code.hpp>
#include <thread>

namespace fs = boost::filesystem;
namespace chrono = boost::chrono;

boost::atomic<int> counter(0);

void thread_function() {
    for (int i = 0; i < 1000; ++i) {
        counter.fetch_add(1, boost::memory_order_relaxed);
    }
}

int main() {
    fs::current_path();
    
    boost::system::error_code ec;
    fs::exists("/tmp", ec);
    
    auto start = chrono::steady_clock::now();
    
    boost::thread t1(thread_function);
    boost::thread t2(thread_function);
    
    t1.join();
    t2.join();
    
    auto end = chrono::steady_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);
    
    return 0;
}