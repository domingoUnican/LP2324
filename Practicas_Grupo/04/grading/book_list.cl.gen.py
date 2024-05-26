from Base_clases import *


class Book(IO):
    def __init__(self):
        super().__init__()
        self.title: String = String()
        self.author: String = String()


    @mutable_params
    def initBook(self, title_p: Par['String'], author_p: Par['String']) -> 'Book':
        def _block1():
            self.title = _var1 = title_p[:]
            _var1
            self.author = _var2 = author_p[:]
            _var2
            return self

        return _block1()

    @mutable_params
    def print(self, ) -> 'Book':
        def _block1():
            self.out_string(String("title:      ")).out_string(self.title).out_string(String("\n"))
            self.out_string(String("author:     ")).out_string(self.author).out_string(String("\n"))
            return self

        return _block1()

    def copy(self):
        c = Book()
        c.title = self.title
        c.author = self.author
        return c

class Article(Book):
    def __init__(self):
        super().__init__()
        self.per_title: String = String()


    @mutable_params
    def initArticle(self, title_p: Par['String'], author_p: Par['String'], per_title_p: Par['String']) -> 'Article':
        def _block1():
            self.initBook(title_p[:], author_p[:])
            self.per_title = _var1 = per_title_p[:]
            _var1
            return self

        return _block1()

    @mutable_params
    def print(self, ) -> 'Book':
        def _block1():
            Book.print(self, )
            self.out_string(String("periodical:  ")).out_string(self.per_title).out_string(String("\n"))
            return self

        return _block1()

    def copy(self):
        c = Article()
        c.per_title = self.per_title
        return c

class BookList(IO):
    @mutable_params
    def isNil(self, ) -> 'Bool':
        def _block1():
            self.abort()
            return true

        return _block1()

    @mutable_params
    def cons(self, hd: Par['Book']) -> 'Cons':
        @mutable_params
        def _let1(new_cell: Par[Cons]):
            return new_cell[:].init(hd[:], self)

        return _let1(Cons())

    @mutable_params
    def car(self, ) -> 'Book':
        def _block1():
            self.abort()
            return Book()

        return _block1()

    @mutable_params
    def cdr(self, ) -> 'BookList':
        def _block1():
            self.abort()
            return BookList()

        return _block1()

    @mutable_params
    def print_list(self, ) -> 'Object':
        return self.abort()



class Cons(BookList):
    def __init__(self):
        super().__init__()
        self.xcar: Book = Void
        self.xcdr: BookList = Void


    @mutable_params
    def isNil(self, ) -> 'Bool':
        return false

    @mutable_params
    def init(self, hd: Par['Book'], tl: Par['BookList']) -> 'Cons':
        def _block1():
            self.xcar = _var1 = hd[:]
            _var1
            self.xcdr = _var2 = tl[:]
            _var2
            return self

        return _block1()

    @mutable_params
    def car(self, ) -> 'Book':
        return self.xcar

    @mutable_params
    def cdr(self, ) -> 'BookList':
        return self.xcdr

    @mutable_params
    def print_list(self, ) -> 'Object':
        def _block1():
            _match1 = check_match(self.xcar.print())
            if isinstance(_match1, Book):
                dummy = _match1
                _match_result1 = self.out_string(String("- dynamic type was Book -\n"))
            elif isinstance(_match1, Article):
                dummy = _match1
                _match_result1 = self.out_string(String("- dynamic type was Article -\n"))
            else:
                _match_result1 = Void
            _match_result1
            return self.xcdr.print_list()

        return _block1()

    def copy(self):
        c = Cons()
        c.xcar = self.xcar
        c.xcdr = self.xcdr
        return c

class Nil(BookList):
    @mutable_params
    def isNil(self, ) -> 'Bool':
        return true

    @mutable_params
    def print_list(self, ) -> 'Object':
        return true



class Main(Object):
    def __init__(self):
        super().__init__()
        self.books: BookList = Void


    @mutable_params
    def main(self, ) -> 'Object':
        @mutable_params
        def _let1(a_book: Par[Book]):
            @mutable_params
            def _let2(an_article: Par[Article]):
                def _block1():
                    self.books = _var1 = (Nil()).cons(a_book[:]).cons(an_article[:])
                    _var1
                    return self.books.print_list()

                return                 _block1()

            return _let2((Article()).initArticle(String("The Top 100 CD_ROMs"), String("Ulanoff"), String("PC Magazine")))

        return _let1((Book()).initBook(String("Compilers, Principles, Techniques, and Tools"), String("Aho, Sethi, and Ullman")))

    def copy(self):
        c = Main()
        c.books = self.books
        return c

if __name__ == '__main__':
    bootstrap(Main)
