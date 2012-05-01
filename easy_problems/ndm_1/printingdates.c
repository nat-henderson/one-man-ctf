// This application prints the current date by asking the kernel to print the date.
// Your goal is to read password.txt, which is owned by the user who wrote 
// and compiled this program.  He has also set the setuid bit.

int main(int argc, char** argv)
{
    setuid( 0 );
    system("date");
    return 0;
}
