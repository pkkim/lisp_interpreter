(def nil (list))

(def filter
	 (lambda (f l)
	   (if (= l nil)
		 nil
		 (if (f (car l))
		   (cons (car l) (filter f (cdr l)))
		   (filter f (cdr l))))))

(def map
	 (lambda (f l)
	   (if (= l nil)
		 nil
		 (cons (f (car l)) (map f (cdr l))))))

(def reduce
	 (lambda (f l init)
	   (if (= l nil)
		 init
		 (reduce f (cdr l) (f init (car l))))))

(def make-acc (lambda (starting) (lambda (incr) ((set starting (+ starting incr)); starting))))
(def prev (lambda (starting) (lambda (next) ((def this starting); (set starting next); this))))

